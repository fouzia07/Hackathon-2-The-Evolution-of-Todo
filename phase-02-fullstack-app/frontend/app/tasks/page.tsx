/**
 * Tasks page - Main application interface.
 *
 * Displays all tasks for the authenticated user with CRUD operations.
 */
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { taskAPI, authAPI, Task, TaskCreate, TaskUpdate } from "@/lib/api";
import TaskCard from "@/components/tasks/TaskCard";
import CreateTaskForm from "@/components/tasks/CreateTaskForm";
import EditTaskForm from "@/components/tasks/EditTaskForm";

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/auth/signin");
      return;
    }

    loadTasks();
  }, [router]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const data = await taskAPI.getTasks();
      setTasks(data);
      setError("");
    } catch (err: any) {
      if (err.response?.status === 401) {
        router.push("/auth/signin");
      } else {
        setError("Failed to load tasks");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData: TaskCreate) => {
    const newTask = await taskAPI.createTask(taskData);
    setTasks([...tasks, newTask]);
    setShowCreateForm(false);
  };

  const handleUpdateTask = async (taskId: number, update: TaskUpdate) => {
    const updatedTask = await taskAPI.updateTask(taskId, update);
    setTasks(tasks.map((t) => (t.id === taskId ? updatedTask : t)));
    setEditingTask(null);
  };

  const handleToggleComplete = async (taskId: number) => {
    const task = tasks.find((t) => t.id === taskId);
    if (!task) return;

    try {
      const updatedTask = await taskAPI.updateTask(taskId, {
        is_complete: !task.is_complete,
      });
      setTasks(tasks.map((t) => (t.id === taskId ? updatedTask : t)));
    } catch (err) {
      setError("Failed to update task");
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      await taskAPI.deleteTask(taskId);
      setTasks(tasks.filter((t) => t.id !== taskId));
    } catch (err) {
      setError("Failed to delete task");
    }
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      router.push("/auth/signin");
    } catch (err) {
      // Even if logout fails, clear token and redirect
      localStorage.removeItem("access_token");
      router.push("/auth/signin");
    }
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === "active") return !task.is_complete;
    if (filter === "completed") return task.is_complete;
    return true;
  });

  const stats = {
    total: tasks.length,
    active: tasks.filter((t) => !t.is_complete).length,
    completed: tasks.filter((t) => t.is_complete).length,
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-sm font-medium text-gray-500">Total Tasks</div>
            <div className="mt-1 text-3xl font-semibold text-gray-900">
              {stats.total}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-sm font-medium text-gray-500">Active</div>
            <div className="mt-1 text-3xl font-semibold text-blue-600">
              {stats.active}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-sm font-medium text-gray-500">Completed</div>
            <div className="mt-1 text-3xl font-semibold text-green-600">
              {stats.completed}
            </div>
          </div>
        </div>

        {/* Actions Bar */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex space-x-2">
            <button
              onClick={() => setFilter("all")}
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                filter === "all"
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
              }`}
            >
              All ({stats.total})
            </button>
            <button
              onClick={() => setFilter("active")}
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                filter === "active"
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
              }`}
            >
              Active ({stats.active})
            </button>
            <button
              onClick={() => setFilter("completed")}
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                filter === "completed"
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
              }`}
            >
              Completed ({stats.completed})
            </button>
          </div>
          <button
            onClick={() => setShowCreateForm(true)}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            + New Task
          </button>
        </div>

        {/* Task List */}
        <div className="space-y-4">
          {filteredTasks.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <p className="text-gray-500">
                {filter === "all"
                  ? "No tasks yet. Create your first task!"
                  : `No ${filter} tasks.`}
              </p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onToggleComplete={handleToggleComplete}
                onEdit={setEditingTask}
                onDelete={handleDeleteTask}
              />
            ))
          )}
        </div>
      </main>

      {/* Modals */}
      {showCreateForm && (
        <CreateTaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowCreateForm(false)}
        />
      )}
      {editingTask && (
        <EditTaskForm
          task={editingTask}
          onSubmit={handleUpdateTask}
          onCancel={() => setEditingTask(null)}
        />
      )}
    </div>
  );
}
