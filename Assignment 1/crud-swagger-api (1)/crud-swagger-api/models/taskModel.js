// In-memory data store.
// Swap this module out for a database layer (MongoDB, PostgreSQL, etc.)
// without changing the routes, as long as the same function signatures are kept.

let nextId = 1;

let tasks = [
  {
    id: nextId++,
    title: 'Learn Swagger',
    description: 'Understand how to document REST APIs with OpenAPI',
    done: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

// Task IDs are sequential integers. Path params arrive as strings, so
// getById/remove normalize with Number(id) before comparing.
const getAll = () => tasks;

const getById = (id) => tasks.find((task) => task.id === Number(id));

const create = ({ title, description = '', done = false }) => {
  const newTask = {
    id: nextId++,
    title,
    description,
    done,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
  tasks.push(newTask);
  return newTask;
};

const update = (id, updates) => {
  const task = getById(id);
  if (!task) return null;

  if (updates.title !== undefined) task.title = updates.title;
  if (updates.description !== undefined) task.description = updates.description;
  if (updates.done !== undefined) task.done = updates.done;
  task.updatedAt = new Date().toISOString();

  return task;
};

const remove = (id) => {
  const index = tasks.findIndex((task) => task.id === Number(id));
  if (index === -1) return false;
  tasks.splice(index, 1);
  return true;
};

module.exports = { getAll, getById, create, update, remove };
