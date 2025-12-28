def greedy_algorithm(items, budget):
    sorted_items = sorted(
        items.items(),
        key=lambda x: x[1]["calories"] / x[1]["cost"],
        reverse=True
    )
    
    selected = []
    total_cost = 0
    total_calories = 0
    
    for name, data in sorted_items:
        if total_cost + data["cost"] <= budget:
            selected.append(name)
            total_cost += data["cost"]
            total_calories += data["calories"]
    
    return selected


def dynamic_programming(items, budget):
    names = list(items.keys())
    item_count = len(names)
    
    costs = [items[name]["cost"] for name in names]
    calories = [items[name]["calories"] for name in names]
    
    dp_table = [[0] * (budget + 1) for _ in range(item_count + 1)]
    
    for item_index in range(1, item_count + 1):
        for current_budget in range(budget + 1):
            if costs[item_index - 1] <= current_budget:
                dp_table[item_index][current_budget] = max(
                    dp_table[item_index - 1][current_budget],
                    dp_table[item_index - 1][current_budget - costs[item_index - 1]] + calories[item_index - 1]
                )
            else:
                dp_table[item_index][current_budget] = dp_table[item_index - 1][current_budget]
    
    selected = []
    remaining_budget = budget
    for item_index in range(item_count, 0, -1):
        if dp_table[item_index][remaining_budget] != dp_table[item_index - 1][remaining_budget]:
            selected.append(names[item_index - 1])
            remaining_budget -= costs[item_index - 1]
    
    return selected

def main():
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }
    
    budget = int(input("Введіть бюджет: "))
    
    greedy_result = greedy_algorithm(items, budget)
    print(f"Жадібний алгоритм: {greedy_result}")
    greedy_calories = sum(items[item]["calories"] for item in greedy_result)
    greedy_cost = sum(items[item]["cost"] for item in greedy_result)
    print(f"Калорії: {greedy_calories}, Вартість: {greedy_cost}")
    
    dp_result = dynamic_programming(items, budget)
    print(f"Динамічне програмування: {dp_result}")
    dp_calories = sum(items[item]["calories"] for item in dp_result)
    dp_cost = sum(items[item]["cost"] for item in dp_result)
    print(f"Калорії: {dp_calories}, Вартість: {dp_cost}")

if __name__ == "__main__":
    raise SystemExit(main())