import random
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter


def analytical_probabilities():
    combinations = {
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 5,
        9: 4, 
        10: 3,
        11: 2,
        12: 1
    }
    
    total = 36

    return {s: c / total for s, c in combinations.items()}


def monte_carlo_simulation(num_rolls: int = 1_000_000):
    sums = [random.randint(1, 6) + random.randint(1, 6) for _ in range(num_rolls)]
    counts = Counter(sums)
    probabilities = {s: counts[s] / num_rolls for s in range(2, 13)}
    
    return probabilities


def create_comparison_table(analytical, monte_carlo):
    data = []
    for s in range(2, 13):
        analytical_prob = analytical[s]
        mc_prob = monte_carlo[s]
        difference = abs(analytical_prob - mc_prob)
        relative_error = (difference / analytical_prob) * 100
        
        data.append({
            'Сума': s,
            'Аналітична ймовірність': f"{analytical_prob:.4f} ({analytical_prob*100:.2f}%)",
            'Монте-Карло': f"{mc_prob:.4f} ({mc_prob*100:.2f}%)",
            'Абсолютна похибка': f"{difference:.6f}",
            'Відносна похибка (%)': f"{relative_error:.2f}%"
        })
    
    return pd.DataFrame(data)


def plot_comparison(analytical: dict, monte_carlo: dict, num_rolls: int):
    sums = list(range(2, 13))
    analytical_probs = [analytical[s] * 100 for s in sums]
    mc_probs = [monte_carlo[s] * 100 for s in sums]
    
    # Налаштування стилю
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Ширина стовпців
    bar_width = 0.35
    x = range(len(sums))
    
    # Стовпчикова діаграма
    bars1 = ax.bar([i - bar_width/2 for i in x], analytical_probs, bar_width, 
                   label='Аналітичні (теоретичні)', color='#2ecc71', edgecolor='black', alpha=0.8)
    bars2 = ax.bar([i + bar_width/2 for i in x], mc_probs, bar_width,
                   label=f'Монте-Карло ({num_rolls:,} кидків)', color='#3498db', edgecolor='black', alpha=0.8)
    
    # Налаштування осей
    ax.set_xlabel('Сума на двох кубиках', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ймовірність (%)', fontsize=12, fontweight='bold')
    ax.set_title('Порівняння ймовірностей сум при киданні двох кубиків\n'
                 'Аналітичний метод vs Метод Монте-Карло', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sums)
    ax.legend(loc='upper right', fontsize=10)
    
    # Додаємо значення над стовпцями
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3), textcoords="offset points",
                   ha='center', va='bottom', fontsize=8, color='#27ae60')
    
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3), textcoords="offset points",
                   ha='center', va='bottom', fontsize=8, color='#2980b9')
    
    plt.tight_layout()
    plt.savefig('monte_carlo_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()


def plot_convergence(max_rolls: int = 100_000, step: int = 1000):
    analytical = analytical_probabilities()
    
    # Симулюємо кидки поступово
    all_sums = []
    roll_counts = []
    errors = []
    
    for i in range(step, max_rolls + 1, step):
        # Додаємо нові кидки
        new_sums = [random.randint(1, 6) + random.randint(1, 6) for _ in range(step)]
        all_sums.extend(new_sums)
        
        # Обчислюємо поточну похибку
        counts = Counter(all_sums)
        mc_probs = {s: counts.get(s, 0) / len(all_sums) for s in range(2, 13)}
        
        # Середня абсолютна похибка
        avg_error = sum(abs(analytical[s] - mc_probs[s]) for s in range(2, 13)) / 11
        
        roll_counts.append(i)
        errors.append(avg_error * 100)
    
    # Побудова графіку
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(roll_counts, errors, color='#e74c3c', linewidth=2)
    ax.fill_between(roll_counts, errors, alpha=0.3, color='#e74c3c')
    
    ax.set_xlabel('Кількість кидків', fontsize=12, fontweight='bold')
    ax.set_ylabel('Середня абсолютна похибка (%)', fontsize=12, fontweight='bold')
    ax.set_title('Збіжність методу Монте-Карло\n'
                 'Зменшення похибки зі збільшенням кількості симуляцій', 
                 fontsize=14, fontweight='bold')
    
    # Логарифмічна шкала для кращої візуалізації
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig('monte_carlo_convergence.png', dpi=150, bbox_inches='tight')
    plt.close()

def wrapped_string(string):
    print("-" * 70)
    print(string)
    print("-" * 70)

def main():
    wrapped_string("Симуляція кидання двох шестигранних кубиків методом Монте-Карло")
    
    NUM_ROLLS = 1_000_000
    analytical = analytical_probabilities()
    monte_carlo = monte_carlo_simulation(NUM_ROLLS)
    
    wrapped_string("Результати порівняння аналітичного методу та методу Монте-Карло")
    
    df = create_comparison_table(analytical, monte_carlo)
    print(df.to_string(index=False))
    
    # Зберігаємо таблицю у CSV
    df.to_csv('results_comparison.csv', index=False, encoding='utf-8-sig')
    
    # Обчислюємо загальну статистику похибок
    total_abs_error = sum(abs(analytical[s] - monte_carlo[s]) for s in range(2, 13))
    avg_abs_error = total_abs_error / 11
    max_error = max(abs(analytical[s] - monte_carlo[s]) for s in range(2, 13))
    
    wrapped_string("Загальна статистика похибок")
    print(f"Середня абсолютна похибка: {avg_abs_error:.6f} ({avg_abs_error*100:.4f}%)")
    print(f"Максимальна абсолютна похибка: {max_error:.6f} ({max_error*100:.4f}%)")
    
    plot_comparison(analytical, monte_carlo, NUM_ROLLS)
    plot_convergence()


if __name__ == "__main__":
    raise SystemExit(main())