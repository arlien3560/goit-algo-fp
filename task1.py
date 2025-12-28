class Node:
  def __init__(self, data=None):
    self.data = data
    self.next = None


class LinkedList:
  def __init__(self):
    self.head = None

  def insert_at_beginning(self, data):
    new_node = Node(data)
    new_node.next = self.head
    self.head = new_node

  def insert_at_end(self, data):
    new_node = Node(data)
    if self.head is None:
      self.head = new_node
    else:
      cur = self.head
      while cur.next:
        cur = cur.next
      cur.next = new_node

  def insert_after(self, prev_node: Node, data):
    if prev_node is None:
      print("Попереднього вузла не існує.")
      return
    new_node = Node(data)
    new_node.next = prev_node.next
    prev_node.next = new_node

  def delete_node(self, key: int):
    cur = self.head
    if cur and cur.data == key:
      self.head = cur.next
      cur = None
      return
    prev = None
    while cur and cur.data != key:
      prev = cur
      cur = cur.next
    if cur is None:
      return
    prev.next = cur.next
    cur = None

  def search_element(self, data: int) -> Node | None:
    cur = self.head
    while cur:
      if cur.data == data:
        return cur
      cur = cur.next
    return None

  def print_list(self):
    current = self.head
    while current:
      print(current.data)
      current = current.next

  # Новий метод: Реверсування зв'язного списку
  def reverse(self):
    prev = None
    current = self.head

    while current:
      next_node = current.next
      current.next = prev
      prev = current
      current = next_node
    
    self.head = prev

  # Новий метод: Сортування вставками
  def insertion_sort(self):
    if not self.head or not self.head.next:
      return
    
    sorted_head = None
    current = self.head
    
    while current:
      next_node = current.next
      sorted_head = self._sorted_insert(sorted_head, current)
      current = next_node
    
    self.head = sorted_head

  def _sorted_insert(self, sorted_head, new_node):
    if not sorted_head or sorted_head.data >= new_node.data:
      new_node.next = sorted_head
      return new_node
    
    current = sorted_head
    
    while current.next and current.next.data < new_node.data:
      current = current.next
    
    new_node.next = current.next
    current.next = new_node
    
    return sorted_head

  # Новий метод: Об'єднання двох відсортованих списків
  @staticmethod
  def merge_sorted_lists(list1: 'LinkedList', list2: 'LinkedList') -> 'LinkedList':
    merged = LinkedList()
    cur1 = list1.head
    cur2 = list2.head
    
    while cur1 and cur2:
      if cur1.data <= cur2.data:
        merged.insert_at_end(cur1.data)
        cur1 = cur1.next
      else:
        merged.insert_at_end(cur2.data)
        cur2 = cur2.next
    
    while cur1:
      merged.insert_at_end(cur1.data)
      cur1 = cur1.next
    
    while cur2:
      merged.insert_at_end(cur2.data)
      cur2 = cur2.next
    
    return merged

def main():
    linked_list = LinkedList()

    linked_list.insert_at_beginning(5)
    linked_list.insert_at_beginning(10)
    linked_list.insert_at_beginning(15)

    linked_list.insert_at_end(20)
    linked_list.insert_at_end(25)

    # Друк зв'язного списку
    print("Зв'язний список:")
    linked_list.print_list()
    print("--------------------")

    # Тест реверсування
    print("Оригінальний список:")
    linked_list.print_list()
    linked_list.reverse()
    print("--------------------")
    print("Reversed list:")
    linked_list.print_list()
    print("--------------------")

    # Тест сортування вставками
    linked_list.insert_at_end(1)
    linked_list.insert_at_end(30)
    print("\nUnsorted list with additions:")
    linked_list.print_list()
    linked_list.insertion_sort()
    print("--------------------")
    print("Sorted list:")
    linked_list.print_list()
    print("--------------------")

    # Test merge
    list1 = LinkedList()
    list1.insert_at_end(1)
    list1.insert_at_end(3)
    list1.insert_at_end(5)
    list2 = LinkedList()
    list2.insert_at_end(2)
    list2.insert_at_end(4)
    list2.insert_at_end(6)
    merged = LinkedList.merge_sorted_lists(list1, list2)
    print("\nMerged sorted list:")
    merged.print_list()

if __name__ == "__main__":
    raise SystemExit(main())