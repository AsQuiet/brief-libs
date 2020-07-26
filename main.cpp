#include <iostream>
#include "briefcpp/brief.hpp"

//
// STACK
//

template <typename T>
class Stack
{
private:
    int stack_size;
    T *ptr;
public:
    Stack();
    void push(T element);
    T pop();
    int size();
    void print();
};

template <typename T>
Stack<T>::Stack()
{
    stack_size = 0;
    ptr = (T*) std::malloc(sizeof(T*));
}

template <typename T>
void Stack<T>::push(T element)
{
    stack_size++;
    ptr =(T*) std::realloc(ptr, sizeof(T*) * stack_size);
    ptr[stack_size-1] = element;
}

template <typename T>
T Stack<T>::pop()
{
    stack_size--;
    T result = ptr[stack_size];
    ptr =(T*) std::realloc(ptr, sizeof(T*) * stack_size);
    return result;
}

template <typename T>
int Stack<T>::size()
{
    return stack_size;
}

template <typename T>
void Stack<T>::print()
{
    for (int i = stack_size - 1; i >= 0; i--)
        std::cout << "    " << ptr[i] << "\n";
}

//
// QUEUE
//

template <typename T>
class Queue
{
private:
    T *ptr;
    int size;
    int max_size = -1;
public:
    Queue();
    
    void set_max_size(int mxs);
    void print();

    void add_last(T element);
    void add_first(T element);

    T remove_last();
    T remove_first();

    T get_element(int index);
    bool contains(T element);
    int get_size();
};

template <typename T>
Queue<T>::Queue()
{
    size = 0;
    ptr = (T*) std::malloc(sizeof(T*));
}

template <typename T>
void Queue<T>::set_max_size(int mxs)
{
    max_size = mxs;
}

template <typename T>
void Queue<T>::add_last(T element)
{
    if (size + 1 >= max_size && max_size != -1)
        throw "Maximum size exceeded.";

    size++;
    ptr = (T*) std::realloc(ptr, sizeof(T) * size);
    ptr[size-1] = element;
}

template <typename T>
void Queue<T>::add_first(T element)
{
    if (size + 1 >= max_size && max_size != -1)
        throw "Maximum size exceeded.";
    
    size++;
    ptr = (T*) std::realloc(ptr, sizeof(T) * size);
    
    
    for (int i = size - 1; i > 0; i--)
        ptr[i] = ptr[i-1];

    ptr[0] = element;

}

template <typename T>
void Queue<T>::print()
{   
    for (int i = 0; i < size; i++) {
        std::cout << ptr[i];
        if (i != size - 1)
            std::cout << ", ";
    }
    std::cout << "\n";
}

template <typename T>
T Queue<T>::remove_first()
{
    size--;
    T result = ptr[0];

    for (int i = 0; i < size; i++)
        ptr[i] = ptr[i+1];

    ptr = (T*) std::realloc(ptr, sizeof(T*) * size);
    return result;
}

template <typename T>
T Queue<T>::remove_last()
{
    size--;
    T result = ptr[size];
    ptr = (T*) std::realloc(ptr, sizeof(T) * size);
    return result;
}

template <typename T>
T Queue<T>::get_element(int index)
{
    return ptr[index];
}

template <typename T>
bool Queue<T>::contains(T element)
{
    for (int i = 0; i < size; i++)
        if (element == ptr[i])
            return true;
    return false;
}

template <typename T>
int Queue<T>::get_size()
{
    return size;
}




int main() {

    
    // Stack<int> myStack = Stack<int>();
    // myStack.push(4);
    // myStack.push(43);
    // myStack.push(42);
    
    Queue<int> q = Queue<int>();

    q.add_last(2);
    q.add_last(4);
    q.add_last(4);
    q.add_last(4);
    q.add_first(9);
    q.add_first(12);

    q.print();

    int l = q.remove_last();
    std::cout << l;
    q.print();

    std::cout << q.get_element(2) << q.get_size();

    return 0;
}

