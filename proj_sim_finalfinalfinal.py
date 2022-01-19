from numpy import random
import matplotlib.pyplot as plt



def buy_quan():
    a = random.uniform(0, 1)
    if a <= 0.5:
        v = 1
    elif a <= 0.75:
        v = 2
    elif a <= 0.875:
        v = 3
    else:
        v = 4
    return v


def percent(x1, t):
    a = (sum(x1) / sum(t)) * 100
    return a


min_inventory =  32  #int(input('enter minimum of inventory: '))
max_inventory = 43 #int(input('enter maximum of inventory: '))
initial =  50#int(input('input initial stock: '))
max_clock =  500#int(input('enter simulation duration(in month): '))

fel = [[0, 1], [1, 2]]  # type = 0>> restock , 1>> buying , 2>> check stock
stock = [[initial, 0]]
newev = []
fcount = 0
ncount = 0
ordelist = []
fastorder = []
order = []
delaylist = []
check_count = 0
total_order = 0
delayed_demand = 0
sales = []
discount_sales = []
total_sales = []
costfast = []
costn = []
costinv = []
costdelay = []
not_usable = []
stockfl = [initial]
profitfl = []
total_stock = 0
s = 0
s2 = 0
t = 0

# start of program

while fel[0][0] <= max_clock:
    stock = sorted(stock, key=lambda mo: mo[1])  # sort stock by date and delete zero values
    stock = [y for y in stock if y[0] != 0]
    g = [z[0] for z in stock if fel[0][0] - z[1] > 2]  # collect unusable products
    if len(g) > 0:
        not_usable.append(g)
    stock = [p for p in stock if fel[0][0] - p[1] < 2]  # delete unusable products from stock
    s2, s1 = 0, 0

    # restock, placing products in stock and and answer delayed demands
    if fel[0][1] == 0:
        new_item = []
        if delayed_demand <= order[0][1]:
            new_item = [order[0][1] - delayed_demand, fel[0][0]]
            stock.append(new_item)
            s += delayed_demand * 12
            sales.append(s)
            total_sales.append(s)
            s = 0
            delaylist.append(delayed_demand)
            delayed_demand = 0

        elif delayed_demand > order[0][1]:
            s += order[0][1] * 12
            sales.append(s)
            total_sales.append(s)
            s = 0
            delayed_demand -= order[0][1]

        order.pop(0)
        order.sort()

    # purchase , a customer comes in
    if fel[0][1] == 1:
        quantity = buy_quan()  # generate random value for customer purchase quantity
        b = 0
        while quantity > 0:  # collecting purchases from stock
            if len(stock) == 0:
                zero = [0, 0]
                stock.append(zero)
            if stock[b][0] > 0:
                stock[b][0] -= 1
                quantity -= 1
                if 1 <= fel[0][0] - stock[b][1] <= 2:  # check if product has discount
                    s2 += 6
                elif 0 <= fel[0][0] - stock[b][1] < 1:
                    s += 12
            else:
                b += 1
            if b >= len(stock):  # delay the demand if stock is empty
                delayed_demand += quantity
                quantity = 0
                break
        total_sales.append(s + s2)

        sales.append(s)  # collecting sales
        discount_sales.append(s2)

        s = 0

        newev = [random.exponential(1 / 15) + fel[0][0], 1]  # next customer visit
        fel.append(newev)

    # calculating total stock and orders
    total_stock = 0
    total_order = 0
    for x in range(0, len(stock)):
        total_stock = total_stock + stock[x][0]
    for x in range(0, len(order)):
        total_order = total_order + order[x][1]
    stockfl.append(total_stock - delayed_demand)
    # check stock
    if fel[0][1] == 2:

        c = total_stock * 1
        costinv.append(c)
        c = delayed_demand * 4
        costdelay.append(c)

        # normal delivery order
        if 0 < total_order + total_stock - delayed_demand < min_inventory:
            order_quantity = max_inventory - (total_order + total_stock - delayed_demand)
            ordelist.append(order_quantity)
            arrival_order = random.uniform(0.25, 1.25) + fel[0][0]
            neworder = [arrival_order, order_quantity]
            order.append(neworder)
            order.sort()
            c = (order_quantity * 5) + 60
            costn.append(c)
            newev = [arrival_order, 0]
            ncount +=1
            fel.append(newev)
        # fast delivery order
        elif total_order + total_stock - delayed_demand <= 0:
            order_quantity = max_inventory - (total_order + total_stock - delayed_demand)
            fastorder.append(order_quantity)
            arrival_order = random.uniform(0.1, 0.25) + fel[0][0]
            neworder = [arrival_order, order_quantity]
            order.append(neworder)
            order.sort()
            c2 = (order_quantity * 12) + 120
            costfast.append(c2)
            newev = [arrival_order, 0]
            fel.append(newev)
            fcount +=1
        newev = [1 + fel[0][0], 2]  # next inventory check
        fel.append(newev)

    fel.pop(0)
    fel.sort()

total_unusable = 0
for x in range(0, len(not_usable)):
    total_unusable = total_unusable + not_usable[x][0]

for x in range(0, len(stock)):
    total_stock = total_stock + stock[x][0]
jk = total_stock * 10
# report ***************************************************************
total_item = (sum(sales) / 10) + (sum(discount_sales) / 5)
profit = (sum(total_sales)) - (sum(costn) + sum(costfast) + sum(costinv) + sum(costdelay))
print('*' * 10, 'inventory simulation', '*' * 20)
print('*' * 10, 'costs: ', '*' * 20, '\ntotal cost: ', sum(costn) + sum(costfast) + sum(costinv) + sum(costdelay))
print('normal delivery cost: ', sum(costn), '\nfast delivery cost: ', sum(costfast), '\ninventory cost: ',
      sum(costinv), '\ndelay cost: ', sum(costdelay))
print('costs per month: ', ((sum(costn) + sum(costfast) + sum(costinv) + sum(costdelay)) / max_clock))
print('*' * 10, 'sales: ', '*' * 20, '\ntotal sales: ', sum(total_sales), '\nsales in discount: ',
      percent(discount_sales, total_sales), '%')
print('sales per month: ', ((sum(sales) + sum(discount_sales)) / max_clock))
print('delayed demands', sum(delaylist), (sum(delaylist) / total_item) * 100, '%')
print('-' * 60)
print('total items bought(normal delivery)(fast delivery)', sum(ordelist), sum(fastorder))
print('total products sold (without discount, with discount): ', sum(sales) / 10, sum(discount_sales) / 5)
print('products in inventory(quantity,receive date)', stock)
print('rotten products: ', total_unusable, '  per month: ', (total_unusable / max_clock) )
print('-' * 60, '\ntotal profit:', profit, '--- per month :', (profit / max_clock))
# plot sales and inventory status
# print(profitfl)
plt.plot(total_sales)
plt.ylabel('sales')
# plt.show()
plt.plot(stockfl)
plt.ylabel('inventory')
# plt.show()
print('n count ' , ncount)
print('f count ' , fcount)
a = input('exit')
