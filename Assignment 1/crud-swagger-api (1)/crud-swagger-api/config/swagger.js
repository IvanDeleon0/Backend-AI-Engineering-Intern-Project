const swaggerJsdoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Task CRUD API',
      version: '1.0.0',
      description:
        'A simple CRUD REST API for managing Tasks, built with Express and documented with Swagger (OpenAPI 3.0).',
      contact: {
        name: 'API Support',
      },
    },
    servers: [
      {
        url: 'http://localhost:3000',
        description: 'Local development server',
      },
    ],
    components: {
      schemas: {
        Task: {
          type: 'object',
          required: ['title'],
          properties: {
            id: {
              type: 'integer',
              description: 'Auto-generated sequential unique identifier for the task',
              example: 1,
            },
            title: {
              type: 'string',
              description: 'Title of the task',
              example: 'Buy groceries',
            },
            description: {
              type: 'string',
              description: 'Detailed description of the task',
              example: 'Milk, eggs, bread, and coffee',
            },
            done: {
              type: 'boolean',
              description: 'Whether the task has been completed',
              default: false,
              example: false,
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
              description: 'Timestamp when the task was created',
            },
            updatedAt: {
              type: 'string',
              format: 'date-time',
              description: 'Timestamp when the task was last updated',
            },
          },
        },
        TaskInput: {
          type: 'object',
          required: ['title'],
          properties: {
            title: {
              type: 'string',
              example: 'Buy groceries',
            },
            description: {
              type: 'string',
              example: 'Milk, eggs, bread, and coffee',
            },
            done: {
              type: 'boolean',
              example: false,
            },
          },
        },
        Error: {
          type: 'object',
          properties: {
            message: {
              type: 'string',
              example: 'Task not found',
            },
          },
        },
      },
    },
  },
  // Files containing annotations for the Swagger definition
  apis: ['./routes/*.js'],
};

const swaggerSpec = swaggerJsdoc(options);

module.exports = swaggerSpec;
