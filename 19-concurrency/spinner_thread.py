import itertools
import time
from threading import Thread, Event
from primes import is_prime

"""
spin和slow会并发地执行，主线程会启用一个新线程来执行spin，然后调用slow。

python spinner_thread.py 
spinner object: <Thread(Thread-1 (spin), initial)>
| thinking!
...
Answer: 42  
"""

def spin(msg: str, done: Event) -> None: 
    """
    该函数运行在另一个线程。done参数是一个threading.Event的实例，一个简单的同步线程的对象。
    """
    for char in itertools.cycle(r"\|/-"): # itertools.cycle一次yield出一个字符，这是一个无限循环
        status = f"\r{char} {msg}" # text-mode的动画技巧： 移将光标移回带有回车ASCII控制字符（'\r'）的行首
        print(status, end="", flush=True)
        if done.wait(.1): # 当event被另一线程设置过，该方法返回True；如果timeout后，返回False
            break # 退出无限循环
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="") # 通过空格重写清 空状态行，并将光标移回开始处

def slow() -> int:
    """该函数由主线程调用。调用sleep会阻塞主线程，但GIL被释放，因此spinner线程可以接着运行"""
    # time.sleep(3) # 
    # print(is_prime(5_000_111_000_222_021))
    return is_prime(5_000_111_000_222_021)

def supervisor() -> int: # 会返回slow()的结果
    done = Event() # 协调主线程和spinner线程的关键
    spinner = Thread(target=spin, args=("thinking!", done)) # 创建新线程
    print(f"spinner object: {spinner}") # 展示spinner对象。输出 <Thread(Thread-1, initial)> ，initial是线程状态，表示还未启动
    spinner.start() # 启动spinner线程
    result = slow() # 调用slow()，会阻塞主线程，同时第二个线程会运行spinner动画
    done.set() # 设置Event标签为True，这会终止spin函数中的循环
    spinner.join() # 等待直到spinner线程终止
    return result

def main() -> None:
    result = supervisor()
    print(f"Answer: {result}")

if __name__ == '__main__':
    main()