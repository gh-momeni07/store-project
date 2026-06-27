import tkinter as tk
import csv
from tkinter import messagebox
from datetime import date


# پلت رنگ---------------------------------------------------------------------------------
BG           = "#F8F5F2"      # پس‌زمینه اصلی
PRIMARY      = "#B76E79"      # رنگ اصلی
PRIMARY_DARK = "#8B5E83"      # نسخه تیره‌تر 
TEXT         = "#2D2D2D"      # رنگ متن اصلی
SUBTEXT      = "#6B5B63"      # رنگ متن فرعی / راهنما
ENTRY_BG     = "#FFFFFF"      # پس‌زمینه فیلدهای ورودی
BORDER       = "#D8CFCB"      # رنگ حاشیه‌ها
ERROR        = "#D65A5A"      # رنگ پیام خطا
CARD_BG      = "#FFFFFF"      # پس‌زمینه کارت محصول
SIDEBAR_BG   = "#FFFFFF"      # پس‌زمینه سایدبار
GREEN        = "#3B6D11"      # رنگ متن برای موجود
GREEN_BG     = "#EAF3DE"      # پس‌زمینه برچسب برای موجودی
RED_BG       = "#FCEBEB"      # پس‌زمینه برچسب برای ناموجودی
RED_TXT      = "#791F1F"      # رنگ متن برای ناموجود

# خواندن یوزر ها از فایل csv------------------------------------------------------------------
class User:
    def __init__(self, username, password, balance, role):
        self.username = username
        self.password = password
        self.balance = float(balance)
        self.role = role

users = []

with open("users.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        user = User(
            row["username"],
            row["password"],
            row["balance"],
            row["role"]
        )
        users.append(user)

# خواندن محصولات از فایل csv ----------------------------------------------------------------
class Product:
    def __init__(self, product_id, name, price, stock, category) :
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.category = category

products = []

with open("products.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        product = Product(
            row["product_id"],
            row["name"],
            row["price"],
            row["stock"],
            row["category"]
        )
        products.append(product)

# تغییر نقش کاربری--------------------------------------------------------------------------
def set_role(role):
    selected_role.set(role)
    if role == "مدیر":
        btn_admin.config(bg=PRIMARY_DARK, fg="white")
        btn_buyer.config(bg=BORDER, fg=TEXT)
    else:
        btn_buyer.config(bg=PRIMARY, fg="white")
        btn_admin.config(bg=BORDER, fg=TEXT)
    label_error.config(text="") #پاک کردن خطای قبلی

# نمایش و مخفی کردن پسوورد----------------------------------------------------------------
show_password = False
def toggle():
    global show_password
    show_password = not show_password

    if show_password:
        entry_pass.config(show="")
        btn_eye.config(text="🙈")
    else:
        entry_pass.config(show="*")
        btn_eye.config(text="👁")

# ورود-------------------------------------------------------------------------------------
def login():
    username = entry_user.get().strip()
    password = entry_pass.get()
    role     = selected_role.get()

    if not username or not password:
        label_error.config(text="⚠  لطفاً همه فیلدها را پر کنید")
        return

    for user in users:
        if user.username == username and user.password == password and user.role == role:
            label_error.config(text="")
            win.withdraw()
            if role == "خریدار":
                open_buyer(user)
            else:
                open_admin()
            return

    label_error.config(text="⚠  اطلاعات وارد‌شده اشتباه است")
    entry_pass.delete(0, "end")

# بازگشت به صفحه ورود
def logout(current_window):
    """
    پنجره فعلی (خریدار یا مدیر) را می‌بندد،
    فیلدهای ورود را پاک می‌کند و صفحه ورود را دوباره نمایش می‌دهد.
    """
    current_window.destroy()
    entry_user.delete(0, "end")
    entry_pass.delete(0, "end")
    label_error.config(text="")
    win.deiconify()   # نمایش دوباره پنجره ورود

# ابزار کمکی-------------------------------------------------------------------------------
def price(n): 
    """عدد را به فرمت خوانا با جداکننده هزارتایی و پسوند «ت» برمی‌گرداند."""
    return f"{int(n):,} ت"

def scrollable_frame(parent, bg=BG): 
    """
    یک فریم اسکرول‌پذیر عمودی می‌سازد.
 
    Returns:
        outer: فریم بیرونی که باید pack/grid شود
        inner: فریم داخلی که ویجت‌ها روی آن قرار می‌گیرند
    """
    outer  = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(outer, bg=bg, highlightthickness=0)
    sb     = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)
    sb.pack(side="left", fill="y")
    canvas.pack(side="right", fill="both", expand=True)
    inner  = tk.Frame(canvas, bg=bg)
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())

    inner.bind("<Configure>", _configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>",  #اسکرول با موس
                    lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    return outer, inner

# صفحه ورود سیستم------------------------------------------------------------------------
win = tk.Tk()
try:
    win.state("zoomed")  #ویندوز
except:
    win.attributes("-zoomed", True) 

win.resizable(False, False)
win.title("Online Shop")
win.iconbitmap("icon.ico")
win.configure(bg=BG)

selected_role = tk.StringVar(value="خریدار") #نقش پیش فرض

tk.Label(win, text="ورود به سیستم", font=("Vazirmatn", 40, "bold"),
         fg=PRIMARY_DARK, bg=BG).pack(pady=(30, 4))

tk.Label(win, text="نقش و اطلاعات خود را وارد کنید",
         font=("Vazirmatn", 15), fg=SUBTEXT, bg=BG).pack()

tk.Frame(win, bg=PRIMARY, height=1).pack(fill="x", padx=40, pady=16)

# انتخاب نقش
tk.Label(win, text="نقش کاربری", font=("Vazirmatn", 15),
         fg=TEXT, bg=BG).pack()

role_frame = tk.Frame(win, bg=BG)
role_frame.pack(pady=6)

btn_admin = tk.Button(role_frame, text="🛡  مدیر", font=("Vazirmatn", 20),
                      bg=PRIMARY_DARK, fg="white", relief="flat", bd=0,
                      padx=20, pady=8, cursor="hand2",
                      command=lambda: set_role("مدیر"))
btn_admin.pack(side="right", padx=4)

btn_buyer = tk.Button(role_frame, text="🛒  خریدار", font=("Vazirmatn", 20),
                      bg=PRIMARY, fg="white", relief="flat", bd=0,
                      padx=20, pady=8, cursor="hand2",
                      command=lambda: set_role("خریدار"))
btn_buyer.pack(side="right", padx=4)

# یوزرنیم
vorod_frame = tk.Frame(win, bg=BG)
vorod_frame.pack(anchor='s', pady=30)

tk.Label(vorod_frame, text="نام کاربری", font=("Vazirmatn", 20, "bold"),
         fg=TEXT, bg=BG).grid(column=3, row=1)

entry_user = tk.Entry(vorod_frame, font=("Vazirmatn", 22), justify="center",
                      bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                      relief="flat", bd=0, highlightthickness=1,
                      highlightbackground=BORDER, highlightcolor=PRIMARY)
entry_user.grid(column=2, row=1, padx=10)
entry_user.focus()
entry_user.bind('<Return>', lambda event: entry_pass.focus())

# پسورد 
tk.Label(vorod_frame, text="رمز عبور", font=("Vazirmatn", 20, "bold"),
         fg=TEXT, bg=BG).grid(column=3, row=2)

entry_pass = tk.Entry(vorod_frame, font=("Vazirmatn", 22), justify="center",
                      bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                      relief="flat", bd=0, highlightthickness=1,
                      highlightbackground=BORDER, highlightcolor=PRIMARY, show="*")
entry_pass.grid(column=2, row=2, padx=10, pady=20)

btn_eye = tk.Button(vorod_frame, text="👁", font=("Segoe UI Emoji", 11),
                    bg=BG, fg=PRIMARY_DARK,activebackground=BG,activeforeground=PRIMARY,
                    relief="flat", bd=0,
                    cursor="hand2", command=toggle)
btn_eye.grid(column=1, row=2, padx=5)

# خطا 
label_error = tk.Label(win, text="", font=("Vazirmatn", 10),
                        fg=ERROR, bg=BG)
label_error.pack(pady=8)

# ورود 
btn_login = tk.Button(win, text="ورود", font=("Vazirmatn", 22, "bold"),
                      bg=PRIMARY, fg="white", activebackground=PRIMARY_DARK,activeforeground="white",
                      relief="flat", bd=0, cursor="hand2", pady=10,
                      command=login)
btn_login.pack(fill='x', ipady=4,padx=500, pady=30)

# صفحه خریدار-----------------------------------------------------------------------------
def open_buyer(user):
    win.withdraw()
    win_buyer = tk.Toplevel()
    try:
        win_buyer.state("zoomed")
    except:
        win_buyer.attributes("-zoomed", True)

    win_buyer.resizable(False, False)
    win_buyer.title("Online Shop")
    win_buyer.iconbitmap("icon.ico")
    win_buyer.configure(bg=BG)

    cart        = {}                          # {product_id: تعداد}
    filter_cat  = tk.StringVar(value="همه")  # دسته‌بندی انتخابی فعلی
    search_var  = tk.StringVar()             # متن جستجو
    balance_var = tk.DoubleVar(value=user.balance)  # موجودی قابل بروزرسانی

    # نوار بالا
    top_frame = tk.Frame(win_buyer,  bg=PRIMARY, height=55)
    top_frame.pack(fill="x")
    top_frame.pack_propagate(False)

    tk.Label(top_frame, text=" 🛒فروشگاه آنلاین", font=("Vazirmatn", 15, "bold"),
         fg="white", bg=PRIMARY).pack(side="right", padx=20, pady=10)
    
    tk.Button(top_frame, text= "خروج", font=("Vazirmatn", 11),
              fg=PRIMARY_DARK, bg="white",
              activebackground=BORDER, activeforeground=PRIMARY_DARK,
              relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
              command=lambda: logout(win_buyer)
              ).pack(side="left", padx=4)
    
    cart_btn = tk.Button(top_frame, font=("Vazirmatn", 11, "bold"),
                         fg=PRIMARY_DARK, bg="white", relief="flat",
                         bd=0, padx=12, pady=4, cursor="hand2")
    cart_btn.pack(side="left", padx=4)

    def refresh_cart_btn():
        """متن دکمه سبد خرید را با تعداد آیتم‌های فعلی بروز می‌کند."""
        cart_btn.config(text=f"🛒  سبد خرید ({sum(cart.values())})")

    refresh_cart_btn()

    tk.Label(top_frame, text=f"👤  {user.username}",
             font=("Vazirmatn", 11), fg="white", bg=PRIMARY
             ).pack(side="left", padx=8)
    
    balance_lbl = tk.Label(top_frame, font=("Vazirmatn", 11),
                            fg="white", bg=PRIMARY_DARK, padx=10, pady=4)
    balance_lbl.pack(side="left", padx=4)
    
    def refresh_balance():
        """لیبل موجودی را با مقدار فعلی بروز می‌کند."""
        balance_lbl.config(text=f"💰  {price(balance_var.get())}")

    refresh_balance()
    
    # بدنه
    body = tk.Frame(win_buyer, bg=BG)
    body.pack(fill="both", expand=True)

    # سایدبار
    sidebar = tk.Frame(body, bg=SIDEBAR_BG, width=160,
                       highlightthickness=1, highlightbackground=BORDER)
    sidebar.pack(side="right", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="دسته‌بندی", font=("Vazirmatn", 10),
             fg=SUBTEXT, bg=SIDEBAR_BG).pack(anchor="e", padx=12, pady=(14, 6))

    categories  = ["همه"] + sorted({product.category for product in products})
    cat_buttons = {}

    def select_cat(cat):
        """دسته انتخابی را تغییر داده و لیست محصولات را فیلتر می‌کند."""
        filter_cat.set(cat)
        for c, b in cat_buttons.items():
            active = c == cat
            b.config(bg="#FBEAF0" if active else SIDEBAR_BG,
                     fg=PRIMARY_DARK if active else TEXT,
                     font=("Vazirmatn", 12, "bold") if active else ("Vazirmatn", 12))
        render_products()

    for cat in categories:
        first = cat == "همه"
        b = tk.Button(sidebar, text=cat,
                      font=("Vazirmatn", 12, "bold") if first else ("Vazirmatn", 12),
                      bg="#FBEAF0" if first else SIDEBAR_BG,
                      fg=PRIMARY_DARK if first else TEXT,
                      relief="flat", bd=0, padx=10, pady=6,
                      cursor="hand2", anchor="e",
                      command=lambda c=cat: select_cat(c))
        b.pack(fill="x", padx=6)
        cat_buttons[cat] = b

    tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=10, pady=10)

    tk.Label(sidebar, text="فیلتر قیمت (ت)", font=("Vazirmatn", 10),
             fg=SUBTEXT, bg=SIDEBAR_BG).pack(anchor="e", padx=12, pady=(0, 6))

    pf = tk.Frame(sidebar, bg=SIDEBAR_BG)
    pf.pack(fill="x", padx=8)

    price_min = tk.Entry(pf, font=("Vazirmatn", 10), justify="center",
                         bg=ENTRY_BG, fg=TEXT, relief="flat",
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=PRIMARY, width=8)
    price_min.insert(0, "0")
    price_min.pack(side="right", padx=2)

    tk.Label(pf, text="تا", font=("Vazirmatn", 10),
             fg=SUBTEXT, bg=SIDEBAR_BG).pack(side="right")

    price_max = tk.Entry(pf, font=("Vazirmatn", 10), justify="center",
                         bg=ENTRY_BG, fg=TEXT, relief="flat",
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=PRIMARY, width=8)
    price_max.insert(0, "9999999")
    price_max.pack(side="right", padx=2)

    tk.Button(sidebar, text="اعمال فیلتر", font=("Vazirmatn", 10),
              bg=PRIMARY, fg="white", relief="flat", bd=0,
              cursor="hand2", pady=5,
              command=lambda: render_products()
              ).pack(fill="x", padx=8, pady=6)
    
    # سبد خرید
    cart_panel = tk.Frame(body, bg=SIDEBAR_BG, width=210,
                          highlightthickness=1, highlightbackground=BORDER)
    cart_panel.pack(side="left", fill="y")
    cart_panel.pack_propagate(False)

    tk.Label(cart_panel, text="🛒  سبد خرید",
             font=("Vazirmatn", 13, "bold"), fg=PRIMARY_DARK, bg=SIDEBAR_BG
             ).pack(anchor="e", padx=14, pady=(14, 8))
    tk.Frame(cart_panel, bg=BORDER, height=1).pack(fill="x", padx=8)

    # فریم اسکرول‌پذیر برای آیتم‌های سبد
    cart_scroll_outer, cart_items_frame = scrollable_frame(cart_panel, bg=SIDEBAR_BG)
    cart_scroll_outer.pack(fill="both", expand=True)

    # پایین پنل سبد: جمع کل + وضعیت موجودی + دکمه ثبت سفارش
    cart_bottom = tk.Frame(cart_panel, bg=SIDEBAR_BG)
    cart_bottom.pack(fill="x", side="bottom", padx=10, pady=10)
    tk.Frame(cart_bottom, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

    total_lbl  = tk.Label(cart_bottom, text="جمع کل: ۰ ت",
                           font=("Vazirmatn", 11, "bold"),
                           fg=PRIMARY_DARK, bg=SIDEBAR_BG, anchor="e")
    total_lbl.pack(fill="x")

    afford_lbl = tk.Label(cart_bottom, text="",
                           font=("Vazirmatn", 10), bg=SIDEBAR_BG, anchor="e")
    afford_lbl.pack(fill="x", pady=(2, 6))

    # دیکشنری سریع برای دسترسی به محصول با product_id
    PRODUCTS_MAP = {p.product_id : p for p in products} 

    def checkout():
        """
        سفارش را نهایی می‌کند:
        - موجودی کاربر را کم می‌کند
        - سفارش را در orders.csv ذخیره می‌کند
        - موجودی انبار محصولات را کاهش می‌دهد
        - سبد خرید را خالی می‌کند
        """
        total = sum(PRODUCTS_MAP[pid].price * n for pid, n in cart.items())
        if total == 0:
            messagebox.showinfo("سبد خرید", "سبد خرید خالی است!", parent=win_buyer)
            return
        if total > balance_var.get():
            messagebox.showerror("خطا", "موجودی کافی نیست!", parent=win_buyer)
            return
        
        # کاهش موجودی کاربر و ذخیره در users.csv
        user.balance = balance_var.get() - total
        balance_var.set(user.balance)

        with open("users.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "password", "balance", "role"])
            writer.writeheader()
            for u in users:
                writer.writerow({
                    "username": u.username,
                    "password": u.password,
                    "balance" : u.balance,
                    "role"    : u.role
                })

        # ثبت سفارش ها در فایل orders.csv
        today = date.today().strftime("%Y-%m-%d")

        with open("orders.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "product_id", "quantity", "total_price", "date"])
            for pid, n in cart.items():
                writer.writerow({
                    "username"   : user.username,
                    "product_id" : pid,
                    "quantity"   : n,
                    "total_price": PRODUCTS_MAP[pid].price * n,
                    "date"       : today
                })

        # کاهش موجودی انبار و ذخیره در products.csv
        with open("products.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["product_id", "name", "price", "stock", "category"])
            writer.writeheader()
            for p in products:
                writer.writerow({
                    "product_id": p.product_id,
                    "name"      : p.name,
                    "price"     : p.price,
                    "stock"     : p.stock,
                    "category"  : p.category
                })

        refresh_balance()
        cart.clear()
        refresh_cart_ui()
        refresh_cart_btn()
        messagebox.showinfo("✅  ثبت سفارش",
                            f"سفارش با موفقیت ثبت شد!\nمبلغ: {price(total)}",
                            parent=win_buyer)

    tk.Button(cart_bottom, text="ثبت سفارش ✓",
              font=("Vazirmatn", 13, "bold"),
              bg=PRIMARY, fg="white",
              activebackground=PRIMARY_DARK, activeforeground="white",
              relief="flat", bd=0, cursor="hand2", pady=8,
              command=checkout).pack(fill="x")
    
    # وسط صفحه
    center = tk.Frame(body, bg=BG)
    center.pack(side="right", fill="both", expand=True)

    tab_frame = tk.Frame(center, bg=BG)
    tab_frame.pack(fill="x", padx=16, pady=(12, 0))

    tab_products_frame = tk.Frame(center, bg=BG)
    tab_orders_frame   = tk.Frame(center, bg=BG)

    def switch_tab(tab):
        """بین تب محصولات و تب سفارش‌ها سوئیچ می‌کند."""
        if tab == "products":
            tab_products_frame.pack(fill="both", expand=True, padx=8)
            tab_orders_frame.pack_forget()
            btn_tab_p.config(bg="#FBEAF0", fg=PRIMARY_DARK, font=("Vazirmatn", 12, "bold"))
            btn_tab_o.config(bg=BG,        fg=SUBTEXT,      font=("Vazirmatn", 12))
        else:
            tab_orders_frame.pack(fill="both", expand=True, padx=8)
            tab_products_frame.pack_forget()
            btn_tab_o.config(bg="#FBEAF0", fg=PRIMARY_DARK, font=("Vazirmatn", 12, "bold"))
            btn_tab_p.config(bg=BG,        fg=SUBTEXT,      font=("Vazirmatn", 12))
            build_orders_tab()

    btn_tab_p = tk.Button(tab_frame, text="محصولات",
                        font=("Vazirmatn", 12, "bold"),
                        bg="#FBEAF0", fg=PRIMARY_DARK,
                        relief="flat", bd=0, padx=14, pady=6,
                        cursor="hand2", command=lambda: switch_tab("products"))
    btn_tab_p.pack(side="right", padx=3)

    btn_tab_o = tk.Button(tab_frame, text="📋  سفارش‌های من",
                        font=("Vazirmatn", 12),
                        bg=BG, fg=SUBTEXT,
                        relief="flat", bd=0, padx=14, pady=6,
                        cursor="hand2", command=lambda: switch_tab("orders"))
    btn_tab_o.pack(side="right", padx=3)

    tab_products_frame.pack(fill="both", expand=True, padx=8)

    toolbar = tk.Frame(tab_products_frame, bg=BG)
    toolbar.pack(fill="x", pady=10)

    search_entry = tk.Entry(toolbar, textvariable=search_var,
                            font=("Vazirmatn", 13), justify="right",
                            bg=ENTRY_BG, fg=SUBTEXT, insertbackground=TEXT,
                            relief="flat", highlightthickness=1,
                            highlightbackground=BORDER, highlightcolor=PRIMARY)
    search_entry.insert(0, "جستجوی محصول...")
    search_entry.pack(side="right", fill="x", expand=True, ipady=5, padx=(0, 4))

    def si(e):
        """placeholder را هنگام فوکوس پاک می‌کند."""
        if search_entry.get() == "جستجوی محصول...":
            search_entry.delete(0, "end")
            search_entry.config(fg=TEXT)
    def so(e):
        """در صورت خالی بودن، placeholder را بازمی‌گرداند."""
        if not search_entry.get():
            search_entry.insert(0, "جستجوی محصول...")
            search_entry.config(fg=SUBTEXT)

    search_entry.bind("<FocusIn>", si)
    search_entry.bind("<FocusOut>", so)
    search_var.trace_add("write", lambda *_: render_products()) #جستجوی زنده

    # فریم اسکرول‌پذیر برای کارت‌های محصول
    products_scroll_outer, products_inner = scrollable_frame(tab_products_frame, bg=BG)
    products_scroll_outer.pack(fill="both", expand=True)

    COLS = 3

    def filtered_products():
        """
        محصولات را بر اساس دسته، متن جستجو و بازه قیمت فیلتر می‌کند.
        Returns: لیست محصولات فیلترشده
        """
        cat  = filter_cat.get()
        sval = search_var.get().strip()
        if sval == "جستجوی محصول...": sval = ""
        try:
            pmin = float(price_min.get().replace(",", "") or 0)
            pmax = float(price_max.get().replace(",", "") or 9999999)
        except ValueError:
            pmin, pmax = 0, 9999999

        result = [p for p in products
                  if (cat == "همه" or p.category == cat)
                  and (sval == "" or sval.lower() in p.name.lower())
                  and pmin <= p.price <= pmax]
        
        return result
    
    def add_to_cart(pid):
        """
        یک واحد از محصول را به سبد خرید اضافه می‌کند.
        اگر تعداد درخواستی از موجودی انبار بیشتر باشد، هشدار نشان می‌دهد.
        """
        if cart.get(pid, 0) >= PRODUCTS_MAP[pid].stock:
            messagebox.showwarning("موجودی", "موجودی انبار کافی نیست!", parent=win_buyer)
            return
        cart[pid] = cart.get(pid, 0) + 1
        PRODUCTS_MAP[pid].stock -= 1        
        refresh_cart_ui()
        refresh_cart_btn()
        render_products()
        

    def build_orders_tab():
        """
        یک واحد از محصول را به سبد خرید اضافه می‌کند.
        اگر تعداد درخواستی از موجودی انبار بیشتر باشد، هشدار نشان می‌دهد.
        """
        # پاک‌سازی محتوای قبلی
        for w in tab_orders_frame.winfo_children():
            w.destroy()
 
        # خواندن سفارش‌های کاربر جاری
        try:
            orders = []
            with open("orders.csv", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row["username"] == user.username:
                        orders.append(row)
        except FileNotFoundError:
            orders = []
 
        # نمایش پیام «هنوز سفارشی ثبت نشده» در صورت خالی بودن
        if not orders:
            tk.Label(tab_orders_frame, text="هنوز سفارشی ثبت نشده.",
                     font=("Vazirmatn", 13), fg=SUBTEXT, bg=BG).pack(pady=60)
            return
 
        # تعریف ستون‌ها: (عنوان, عرض به پیکسل)
        cols_info = [("شناسه", 80), ("نام محصول", 150), ("تعداد", 60),
                     ("مبلغ کل", 130), ("تاریخ", 110)]
 
        # ردیف هدر جدول
        hdr_row = tk.Frame(tab_orders_frame, bg=PRIMARY)
        hdr_row.pack(fill="x", pady=(10, 0))
        for label, w in cols_info:
            tk.Label(hdr_row, text=label, font=("Vazirmatn", 11, "bold"),
                     fg="white", bg=PRIMARY, width=w // 8,
                     anchor="center", pady=7).pack(side="right", padx=4)
 
        # فریم اسکرول‌پذیر برای ردیف‌های سفارش
        so, si = scrollable_frame(tab_orders_frame, bg=BG)
        so.pack(fill="both", expand=True)
 
        # رندر هر سفارش به عنوان یک ردیف در جدول
        for idx, o in enumerate(orders):
            rbg = CARD_BG if idx % 2 == 0 else BG  # رنگ‌بندی یک‌در‌میان
            r   = tk.Frame(si, bg=rbg, highlightthickness=1, highlightbackground=BORDER)
            r.pack(fill="x", pady=1)
 
            # پیدا کردن نام محصول؛ اگر حذف شده باشد، ID را نشان می‌دهد
            prod  = PRODUCTS_MAP.get(o["product_id"])
            pname = prod.name if prod else o["product_id"]
 
            vals = [o["product_id"], pname, o["quantity"],
                    price(float(o["total_price"])), o["date"]]
 
            # رندر هر سلول به ترتیب ستون‌ها (راست به چپ)
            for v, (_, w) in zip(vals, cols_info):
                tk.Label(r, text=str(v), font=("Vazirmatn", 11),
                         fg=TEXT, bg=rbg, width=w // 8,
                         anchor="center", pady=6).pack(side="right", padx=4)


    def render_products():
        """محصولات فیلتر شده را نمایش میدهد."""
        for w in products_inner.winfo_children():
            w.destroy()

        prods = filtered_products()
        if not prods:
            tk.Label(products_inner, text="محصولی یافت نشد.",
                     font=("Vazirmatn", 13), fg=SUBTEXT, bg=BG
                     ).pack(pady=40)
            return

        for i, p in enumerate(prods):
            row_idx, col = divmod(i, COLS)

            card = tk.Frame(products_inner, bg=CARD_BG,
                            highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=row_idx, column=col, padx=8, pady=8, sticky="nsew")
            products_inner.grid_columnconfigure(col, weight=1)

            hdr = tk.Frame(card, bg=PRIMARY, height=70)
            hdr.pack(fill="x")
            hdr.pack_propagate(False)
            tk.Label(hdr, text=p.name[0], font=("Vazirmatn", 28, "bold"),
                     fg="white", bg=PRIMARY).pack(expand=True)

            bd = tk.Frame(card, bg=CARD_BG)
            bd.pack(fill="x", padx=10, pady=8)

            tk.Label(bd, text=p.name, font=("Vazirmatn", 12, "bold"),
                     fg=TEXT, bg=CARD_BG, anchor="e").pack(fill="x")
            tk.Label(bd, text=f"{p.category}  ·  {p.product_id}",
                     font=("Vazirmatn", 9), fg=SUBTEXT, bg=CARD_BG,
                     anchor="e").pack(fill="x")
            tk.Label(bd, text=price(p.price),
                     font=("Vazirmatn", 12, "bold"), fg=PRIMARY_DARK,
                     bg=CARD_BG, anchor="e").pack(fill="x", pady=(4, 0))

            foot = tk.Frame(bd, bg=CARD_BG)
            foot.pack(fill="x", pady=(6, 2))

            if p.stock > 0:
                tk.Label(foot, text=f"موجود: {p.stock}", font=("Vazirmatn", 9),
                         fg=GREEN, bg=GREEN_BG, padx=6, pady=2).pack(side="right")
                tk.Button(foot, text="+ افزودن",
                          font=("Vazirmatn", 10, "bold"),
                          bg=PRIMARY, fg="white",
                          activebackground=PRIMARY_DARK, activeforeground="white",
                          relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
                          command=lambda pid=p.product_id: add_to_cart(pid)
                          ).pack(side="left")
            else:
                tk.Label(foot, text="ناموجود", font=("Vazirmatn", 9),
                         fg=RED_TXT, bg=RED_BG, padx=6, pady=2).pack(side="right")
                
    def refresh_cart_ui():
        """
        پنل سبد خرید را از ابتدا می‌سازد:
        - برای هر آیتم: نام، قیمت کل و دکمه‌های + و -
        - جمع کل و وضعیت کفایت موجودی را بروز می‌کند
        """
        for w in cart_items_frame.winfo_children():
            w.destroy()

        total = 0
        for pid, n in cart.items():
            p          = PRODUCTS_MAP[pid]
            item_total = p.price * n
            total     += item_total

            row = tk.Frame(cart_items_frame, bg=SIDEBAR_BG)
            row.pack(fill="x", padx=8, pady=4)

            tk.Label(row, text=p.name, font=("Vazirmatn", 11),
                     fg=TEXT, bg=SIDEBAR_BG, anchor="e").pack(fill="x")

            sub = tk.Frame(row, bg=SIDEBAR_BG)
            sub.pack(fill="x")

            tk.Label(sub, text=price(item_total), font=("Vazirmatn", 10),
                     fg=SUBTEXT, bg=SIDEBAR_BG).pack(side="right")

            qf = tk.Frame(sub, bg=SIDEBAR_BG)
            qf.pack(side="left")

            def make_dec(pid=pid):
                """برای دکمه کاهش محصول"""
                def _():
                    PRODUCTS_MAP[pid].stock += 1 
                    if cart.get(pid, 0) > 1:
                        cart[pid] -= 1
                    else: 
                        del cart[pid] # اگر تعداد به صفر رسید، از سبد حذف شود
                    refresh_cart_ui()
                    refresh_cart_btn()
                    render_products()
                return _

            tk.Button(qf, text="−", font=("Vazirmatn", 10), bg=BG, fg=TEXT,
                      relief="flat", bd=0, cursor="hand2", padx=4,
                      command=make_dec()).pack(side="left")
            tk.Label(qf, text=str(n), font=("Vazirmatn", 11, "bold"),
                     fg=TEXT, bg=SIDEBAR_BG, width=2, anchor="center").pack(side="left")
            tk.Button(qf, text="+", font=("Vazirmatn", 10), bg=BG, fg=TEXT,
                      relief="flat", bd=0, cursor="hand2", padx=4,
                      command=lambda pid=pid: add_to_cart(pid)).pack(side="left")

            tk.Frame(cart_items_frame, bg=BORDER, height=1).pack(fill="x", padx=8)

        total_lbl.config(text=f"جمع کل: {price(total)}")
        if total == 0:
            afford_lbl.config(text="")
        elif total <= balance_var.get():
            afford_lbl.config(text="✓  موجودی کافی", fg=GREEN)
        else:
            afford_lbl.config(text="✗  موجودی کافی نیست", fg=ERROR)

    render_products()

    # بستن پنجره
    def close_all():
        """هر دو پنجره را بسته و برنامه را خاتمه می‌دهد."""
        win.destroy()
        win_buyer.destroy()  

    win_buyer.protocol("WM_DELETE_WINDOW", close_all)

# صفحه مدیر------------------------------------------------------------------------------
def open_admin():
    win.withdraw()
    win_admin = tk.Toplevel(win) #ویندوز
    try:
        win_admin.state("zoomed")
    except:
        win_admin.attributes("-zoomed", True)

    win_admin.resizable(False, False)
    win_admin.title("Online Shop")
    win_admin.iconbitmap("icon.ico")
    win_admin.configure(bg=BG)

    # نوار بالا
    top_frame = tk.Frame(win_admin, bg=PRIMARY_DARK, height=55)
    top_frame.pack(fill="x")
    top_frame.pack_propagate(False)

    tk.Label(top_frame, text="🛡  پنل مدیریت فروشگاه",
             font=("Vazirmatn", 15, "bold"), fg="white", bg=PRIMARY_DARK
             ).pack(side="right", padx=20, pady=10)
    
    tk.Button(top_frame, text= "خروج", font=("Vazirmatn", 11),
              fg=PRIMARY_DARK, bg="white",
              activebackground=BORDER, activeforeground=PRIMARY_DARK,
              relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
              command=lambda: logout(win_admin)
              ).pack(side="left", padx=12)

    body = tk.Frame(win_admin, bg=BG)
    body.pack(fill="both", expand=True)

    # تب‌بار
    tab_bar = tk.Frame(body, bg=BG)
    tab_bar.pack(fill="x", padx=16, pady=(12, 0))

    tab_products_frame = tk.Frame(body, bg=BG)
    tab_orders_frame   = tk.Frame(body, bg=BG)
    btn_tabs = {}

    def switch_tab(tab):
        """بین تب مدیریت محصولات و تب مشاهده سفارش‌ها سوئیچ می‌کند."""
        if tab == "products":
            tab_products_frame.pack(fill="both", expand=True, padx=8, pady=8)
            tab_orders_frame.pack_forget()
            btn_tabs["products"].config(bg="#FBEAF0", fg=PRIMARY_DARK,
                                        font=("Vazirmatn", 12, "bold"))
            btn_tabs["orders"].config(bg=BG, fg=SUBTEXT, font=("Vazirmatn", 12))
        else:
            tab_orders_frame.pack(fill="both", expand=True, padx=8, pady=8)
            tab_products_frame.pack_forget()
            btn_tabs["orders"].config(bg="#FBEAF0", fg=PRIMARY_DARK,
                                      font=("Vazirmatn", 12, "bold"))
            btn_tabs["products"].config(bg=BG, fg=SUBTEXT, font=("Vazirmatn", 12))
            build_orders_tab()

    btn_tabs["products"] = tk.Button(tab_bar, text="📦  مدیریت محصولات",
                                     font=("Vazirmatn", 12, "bold"),
                                     bg="#FBEAF0", fg=PRIMARY_DARK,
                                     relief="flat", bd=0, padx=14, pady=6,
                                     cursor="hand2",
                                     command=lambda: switch_tab("products"))
    btn_tabs["products"].pack(side="right", padx=3)

    btn_tabs["orders"] = tk.Button(tab_bar, text="📋  مشاهده سفارش‌ها",
                                   font=("Vazirmatn", 12),
                                   bg=BG, fg=SUBTEXT,
                                   relief="flat", bd=0, padx=14, pady=6,
                                   cursor="hand2",
                                   command=lambda: switch_tab("orders"))
    btn_tabs["orders"].pack(side="right", padx=3)

    # تب محصولات
    tab_products_frame.pack(fill="both", expand=True, padx=8, pady=8)

    def save_products_csv():
        """لیست products را کامل در products.csv بازنویسی می‌کند."""
        with open("products.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["product_id","name","price","stock","category"])
            writer.writeheader()
            for p in products:
                writer.writerow({"product_id": p.product_id, "name": p.name,
                                 "price": p.price, "stock": p.stock,
                                 "category": p.category})

    def open_product_form(edit_product=None):
        """
        فرم افزودن یا ویرایش محصول را باز می‌کند.
        اگر edit_product داده شود، فیلدها پیش‌پر می‌شوند و شناسه قابل ویرایش نیست.
        """
        form = tk.Toplevel(win_admin)
        form.title("ویرایش محصول" if edit_product else "افزودن محصول جدید")
        form.configure(bg=BG)
        form.resizable(False, False)
        form.grab_set() #فرم باز شد پنجره پشتی قفل شود

        tk.Label(form,
                 text="ویرایش محصول" if edit_product else "افزودن محصول جدید",
                 font=("Vazirmatn", 18, "bold"), fg=PRIMARY_DARK, bg=BG
                 ).pack(pady=(20, 4), padx=30)
        tk.Frame(form, bg=PRIMARY, height=1).pack(fill="x", padx=20, pady=(0, 16))

        fields_frame = tk.Frame(form, bg=BG)
        fields_frame.pack(padx=30, pady=4)

        def lbl_entry(parent, text, row, default=""):
            tk.Label(parent, text=text, font=("Vazirmatn", 12, "bold"),
                     fg=TEXT, bg=BG, anchor="e").grid(
                         row=row, column=1, sticky="e", pady=6, padx=(0, 8))
            e = tk.Entry(parent, font=("Vazirmatn", 12), justify="center",
                         bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                         relief="flat", highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=PRIMARY, width=22)
            e.insert(0, default)
            e.grid(row=row, column=0, pady=6)
            return e

        d_id  = edit_product.product_id      if edit_product else ""
        d_nm  = edit_product.name            if edit_product else ""
        d_cat = edit_product.category        if edit_product else ""
        d_prc = str(int(edit_product.price)) if edit_product else ""
        d_stk = str(edit_product.stock)      if edit_product else ""

        e_id    = lbl_entry(fields_frame, "شناسه محصول",  0, d_id)
        e_name  = lbl_entry(fields_frame, "نام محصول",    1, d_nm)
        e_cat   = lbl_entry(fields_frame, "دسته‌بندی",    2, d_cat)
        e_price = lbl_entry(fields_frame, "قیمت (تومان)", 3, d_prc)
        e_stock = lbl_entry(fields_frame, "موجودی",       4, d_stk)

        if edit_product:
            e_id.config(state="disabled") # شناسه در حالت ویرایش قابل تغییر نیست

        err_lbl = tk.Label(form, text="", font=("Vazirmatn", 10), fg=ERROR, bg=BG)
        err_lbl.pack()

        def submit():
            """
            اعتبارسنجی فرم و ذخیره محصول:
            - اگر ویرایش: فیلدهای محصول موجود بروز می‌شود
            - اگر افزودن: محصول جدید به لیست اضافه می‌شود (با بررسی تکراری نبودن شناسه)
            """
            pid   = e_id.get().strip()
            name  = e_name.get().strip()
            cat   = e_cat.get().strip()
            prc_s = e_price.get().strip()
            stk_s = e_stock.get().strip()

            if not all([pid, name, cat, prc_s, stk_s]):
                err_lbl.config(text="⚠  همه فیلدها الزامی هستند")
                return
            try:
                prc = float(prc_s)
                stk = int(stk_s)
                if prc < 0 or stk < 0:
                    raise ValueError
            except ValueError:
                err_lbl.config(text="⚠  قیمت و موجودی باید عدد مثبت باشند")
                return

            if edit_product: # بروزرسانی شیء محصول موجود
                edit_product.name     = name
                edit_product.category = cat
                edit_product.price    = prc
                edit_product.stock    = stk
            else: # بررسی تکراری نبودن شناسه قبل از افزودن
                if any(p.product_id == pid for p in products):
                    err_lbl.config(text="⚠  این شناسه قبلاً استفاده شده است")
                    return
                products.append(Product(pid, name, prc, stk, cat))

            save_products_csv()
            render_product_table()
            form.destroy()
            messagebox.showinfo("✅ موفق", "محصول با موفقیت ذخیره شد.", parent=win_admin)

        btn_row = tk.Frame(form, bg=BG)
        btn_row.pack(pady=16, padx=30, fill="x")

        tk.Button(btn_row, text="ذخیره",
                  font=("Vazirmatn", 13, "bold"), bg=PRIMARY, fg="white",
                  activebackground=PRIMARY_DARK, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2", pady=8, padx=20,
                  command=submit).pack(side="right", padx=4)
        tk.Button(btn_row, text="انصراف",
                  font=("Vazirmatn", 12), bg=BORDER, fg=TEXT,
                  relief="flat", bd=0, cursor="hand2", pady=8, padx=16,
                  command=form.destroy).pack(side="right", padx=4)

    def delete_product(prod):
        """تأییدیه می‌گیرد و در صورت تأیید، محصول را از لیست و فایل حذف می‌کند."""
        if messagebox.askyesno("حذف محصول",
                               f"آیا از حذف «{prod.name}» مطمئن هستید؟",
                               parent=win_admin):
            products.remove(prod)
            save_products_csv()
            render_product_table()

    # نوار ابزار جدول
    tbl_toolbar = tk.Frame(tab_products_frame, bg=BG)
    tbl_toolbar.pack(fill="x", pady=(0, 8))

    tk.Button(tbl_toolbar, text="+ افزودن محصول جدید",
              font=("Vazirmatn", 12, "bold"), bg=PRIMARY, fg="white",
              activebackground=PRIMARY_DARK, activeforeground="white",
              relief="flat", bd=0, cursor="hand2", padx=14, pady=6,
              command=lambda: open_product_form()).pack(side="right")

    COL_DEFS = [
        ("شناسه",      80),
        ("نام محصول", 180),
        ("دسته‌بندی", 120),
        ("قیمت",      120),
        ("موجودی",     80),
        ("عملیات",    160),
    ]

    hdr_bar = tk.Frame(tab_products_frame, bg=PRIMARY_DARK)
    hdr_bar.pack(fill="x")
    for label, w in COL_DEFS:
        tk.Label(hdr_bar, text=label, font=("Vazirmatn", 11, "bold"),
                 fg="white", bg=PRIMARY_DARK, width=w // 8,
                 anchor="center", pady=8).pack(side="right", padx=4)

    tbl_scroll_outer, tbl_inner = scrollable_frame(tab_products_frame, bg=BG)
    tbl_scroll_outer.pack(fill="both", expand=True)

    def render_product_table():
        """
        جدول محصولات را از ابتدا می‌سازد.
        هر ردیف شامل اطلاعات محصول + دکمه‌های ویرایش و حذف است.
        موجودی صفر با رنگ قرمز نمایش داده می‌شود.
        """
        for w in tbl_inner.winfo_children():
            w.destroy()
        if not products:
            tk.Label(tbl_inner, text="هیچ محصولی وجود ندارد.",
                     font=("Vazirmatn", 13), fg=SUBTEXT, bg=BG).pack(pady=40)
            return

        for idx, p in enumerate(products):
            rbg = CARD_BG if idx % 2 == 0 else BG
            row = tk.Frame(tbl_inner, bg=rbg,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=1)

            vals = [p.product_id, p.name, p.category, price(p.price), str(p.stock)]
            for v, (_, w) in zip(vals, COL_DEFS[:-1]):
                lbl_color = (GREEN if p.stock > 0 else RED_TXT) if v == str(p.stock) else TEXT
                tk.Label(row, text=v, font=("Vazirmatn", 11),
                         fg=lbl_color, bg=rbg, width=w // 8,
                         anchor="center", pady=7).pack(side="right", padx=4)

            ops = tk.Frame(row, bg=rbg)
            ops.pack(side="left", padx=8)

            tk.Button(ops, text="ویرایش ✎",
                      font=("Vazirmatn", 9, "bold"), bg=PRIMARY, fg="white",
                      activebackground=PRIMARY_DARK, activeforeground="white",
                      relief="flat", bd=0, cursor="hand2", padx=8, pady=4,
                      command=lambda prod=p: open_product_form(prod)
                      ).pack(side="left", padx=2, pady=4)

            tk.Button(ops, text="حذف ✕",
                      font=("Vazirmatn", 9), bg=RED_BG, fg=RED_TXT,
                      activebackground="#f5c6c6", activeforeground=RED_TXT,
                      relief="flat", bd=0, cursor="hand2", padx=8, pady=4,
                      command=lambda prod=p: delete_product(prod)
                      ).pack(side="left", padx=2, pady=4)

    render_product_table()

    # تب سفارش ها
    def build_orders_tab():
        """
        تب سفارش‌ها را برای مدیر می‌سازد:
        - همه سفارش‌ها از orders.csv خوانده می‌شوند
        - فیلتر بر اساس نام کاربر
        - جدول با ستون‌های کاربر، کالا، نام، تعداد، مبلغ، تاریخ
        - نوار خلاصه در پایین: تعداد سفارش و مجموع فروش
        """
        for w in tab_orders_frame.winfo_children():
            w.destroy()

        try:
            all_orders = []
            with open("orders.csv", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    all_orders.append(row)
        except FileNotFoundError:
            all_orders = []

        # نوار فیلتر
        filter_bar = tk.Frame(tab_orders_frame, bg=BG)
        filter_bar.pack(fill="x", pady=(0, 8))

        tk.Label(filter_bar, text="فیلتر کاربر:",
                 font=("Vazirmatn", 11), fg=TEXT, bg=BG).pack(side="right", padx=(0, 6))

        user_filter_var = tk.StringVar(value="همه")
        usernames = ["همه"] + sorted({o["username"] for o in all_orders})

        user_menu = tk.OptionMenu(filter_bar, user_filter_var, *usernames)
        user_menu.config(font=("Vazirmatn", 10), bg=ENTRY_BG, fg=TEXT,
                         relief="flat", highlightthickness=1,
                         highlightbackground=BORDER, activebackground="#FBEAF0")
        user_menu["menu"].config(font=("Vazirmatn", 10))
        user_menu.pack(side="right")

        PRODUCTS_MAP_ADM = {p.product_id: p for p in products}

        ord_cols = [
            ("کاربر",      110),
            ("شناسه کالا",  90),
            ("نام محصول",  160),
            ("تعداد",       60),
            ("مبلغ کل",    130),
            ("تاریخ",      110),
        ]

        hdr2 = tk.Frame(tab_orders_frame, bg=PRIMARY_DARK)
        hdr2.pack(fill="x")
        for label, w in ord_cols:
            tk.Label(hdr2, text=label, font=("Vazirmatn", 11, "bold"),
                     fg="white", bg=PRIMARY_DARK, width=w // 8,
                     anchor="center", pady=8).pack(side="right", padx=4)

        ord_scroll_outer, ord_inner = scrollable_frame(tab_orders_frame, bg=BG)
        ord_scroll_outer.pack(fill="both", expand=True)

        # خلاصه آماری پایین صفحه
        summary_bar = tk.Frame(tab_orders_frame, bg=SIDEBAR_BG,
                               highlightthickness=1, highlightbackground=BORDER)
        summary_bar.pack(fill="x", side="bottom")

        total_lbl2 = tk.Label(summary_bar, text="",
                              font=("Vazirmatn", 11, "bold"),
                              fg=PRIMARY_DARK, bg=SIDEBAR_BG, pady=8, padx=16)
        total_lbl2.pack(side="right")

        count_lbl = tk.Label(summary_bar, text="",
                             font=("Vazirmatn", 11),
                             fg=SUBTEXT, bg=SIDEBAR_BG, pady=8, padx=16)
        count_lbl.pack(side="right")

        def render_orders_table(*_):
            """
            جدول سفارش‌ها را بر اساس فیلتر کاربر انتخابی رندر می‌کند.
            مجموع فروش و تعداد سفارش‌های نمایش‌داده‌شده را در نوار پایین بروز می‌کند.
            """
            for w in ord_inner.winfo_children():
                w.destroy()
            ufilter = user_filter_var.get()
            shown   = [o for o in all_orders
                       if ufilter == "همه" or o["username"] == ufilter]

            if not shown:
                tk.Label(ord_inner, text="سفارشی یافت نشد.",
                         font=("Vazirmatn", 13), fg=SUBTEXT, bg=BG).pack(pady=40)
                total_lbl2.config(text="")
                count_lbl.config(text="")
                return

            grand_total = 0
            for idx, o in enumerate(shown):
                rbg = CARD_BG if idx % 2 == 0 else BG
                r   = tk.Frame(ord_inner, bg=rbg,
                               highlightthickness=1, highlightbackground=BORDER)
                r.pack(fill="x", pady=1)
                prod  = PRODUCTS_MAP_ADM.get(o["product_id"])
                pname = prod.name if prod else o["product_id"]
                ttl   = float(o["total_price"])
                grand_total += ttl
                vals = [o["username"], o["product_id"], pname,
                        o["quantity"], price(ttl), o["date"]]
                for v, (_, w) in zip(vals, ord_cols):
                    tk.Label(r, text=str(v), font=("Vazirmatn", 11),
                             fg=TEXT, bg=rbg, width=w // 8,
                             anchor="center", pady=6).pack(side="right", padx=4)

            total_lbl2.config(text=f"مجموع فروش: {price(grand_total)}")
            count_lbl.config(text=f"تعداد سفارش: {len(shown)}")

        user_filter_var.trace_add("write", render_orders_table)
        render_orders_table()

    # بستن پنجره
    def close_all():
        win.destroy()
        win_admin.destroy()  

    win_admin.protocol("WM_DELETE_WINDOW", close_all)


#----------------------------------------------------------------------------
win.mainloop()