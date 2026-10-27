from langchain.tools import tool
from database import LocalSession, Todo
from datetime import datetime


### CRUD Operations for Todo Items


@tool
def create_todo(title: str, description: str = "",priority: str = "medium", due_date:str = ""):
    """
        Create and save a new todo task.
        Args:
            title (str): Short title of the todo task (required).
            description (str): Optional detailed note of the todo task.
            priority (str): 'low','medium' or 'high' (default: 'medium').
            due_date (str): Optional due date for the task in DD-MM-YYYY format.
    """


    task_priority = "medium";
    if priority.lower() in ["low", "medium", "high"]:
        task_priority = priority

    with LocalSession() as session:
        todo = Todo(
            title=title,
            description=description,
            priority=task_priority,
            due_date=due_date,
            created_at=datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Formats the date and time into a string.
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)  # Refresh to get the updated todo with ID
        return f'''
Task created successfully with ID: {todo.id} | Title: {todo.title} | Priority : {todo.priority} | Due Date: {todo.due_date}
'''


@tool 
def list_todos(status: str = "all", priority: str = "all"):
    """
    List all todo tasks. Optionally filter by status or priority.
    Args:
        status(str) : "pending", "in_progress", "done" or "all"
        priority(str) : "low", "medium", "high" or "all"
    """
    with LocalSession() as session:
        query = session.query(Todo)
        if status != "all":
            query = query.filter(Todo.status == status)

        if priority != "all":
            query = query.filter(Todo.priority == priority)

        todos = query.order_by(Todo.id).all();

        if not todos:
            return "No tasks found."

        allTodos = [todo.to_dict() for todo in todos]
        return allTodos

@tool
def update_todos(
    todo_id: int,
    title: str,
    description: str = "",
    status: str = "",
    priority: str = "",
    due_date: str = "",
):
    """
    Update an existing todo by its ID. Only provide the fields you want to change.

    Args:
        todo_id:     ID of the todo to update (required)
        title:       New title (leave empty to keep current)
        description: New description (leave empty to keep current)
        status:      New status — 'pending', 'in_progress', or 'done'
        priority:    New priority — 'low', 'medium', or 'high'
        due_date:    New due date e.g. '2025-12-25'
    """

    with LocalSession() as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return f"Todo with id {todo_id} not found"

        if title:
            todo.title = title
        if description:
            todo.description = description
        if status:
            todo.status = status

        if priority:
            todo.priority = priority

        if due_date:
            todo.due_date = due_date

        session.commit()
        session.refresh(todo)

        return f"""
            Todo: {todo.id} updated !
            {todo.to_dict()}
        """


@tool
def delete_todo(todo_id: int):
    """
    Permanently delete a todo by its ID.

    Args:
        todo_id: ID of the todo to delete (required)
    """
    with LocalSession() as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return f"Todo with id {todo_id} not found"


        #Why save the title before deleting?
        #Because after deletion, you want to return a meaningful success message containing the task title.

        title = todo.title
        session.delete(todo)
        session.commit()

        return f"Todo #{title} deleted successfully !"

