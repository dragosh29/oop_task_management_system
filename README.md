# OOP Task Management System

This repository provides an object-oriented task management system built in Python. It enables user, project, and task management through a structured command-line interface, offering persistent data storage and robust filtering options.

## Features

### User Management
- Create, update, list, and remove users
- Assign projects to users

### Project Management
- Add, modify, list, or remove projects
- Set project descriptions and deadlines
- Manage multiple tasks per project

### Task Management
- Three task types supported: DevTask, QATask, and DocTask
- Tasks can be assigned a priority: Low, Medium, High, or Critical
- Supports task status tracking: Not Started, In Progress, Completed
- Allows updating and deleting tasks, filtering by status or priority

### Persistence
- Data is saved and loaded from JSON files
- Supports deserialization of users, projects, and tasks with ID validation
- Automatically retains the last used IDs for users, projects, and tasks to avoid duplication

## Getting Started

### Clone the Repository

```
git clone https://github.com/yourusername/dragosh29-oop_task_management_system.git
cd dragosh29-oop_task_management_system
```

### Run the Application

```
python main.py
```

Follow the CLI prompts to manage users, projects, and tasks interactively.

## Dependencies

- Python 3.10 or higher
- Standard libraries: json, datetime, enum, typing, os, atexit

## License

This project is licensed under the MIT License.
