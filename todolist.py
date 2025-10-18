tasks = []
def add_task(task_name):
    tasks.append(task_name)
    print('đã thêm công việc: ', task_name)
if __name__ == "__main__":
    print("Chào mừng đến với ứng dụng To-Do List!")
    add_task("Học bài Git và GitHub")
    add_task("Làm bài tập thực hành ở nhà")
