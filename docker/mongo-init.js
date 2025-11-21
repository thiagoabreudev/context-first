// MongoDB initialization script
// Executado automaticamente quando container é criado pela primeira vez

db = db.getSiblingDB('context_first_dev');

// Criar coleções com validação
db.createCollection('projects', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'name', 'context_budget', 'created_at'],
      properties: {
        user_id: { bsonType: 'string' },
        name: { bsonType: 'string' },
        context_budget: { bsonType: 'object' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('demands', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['project_id', 'title', 'description', 'status', 'created_at'],
      properties: {
        project_id: { bsonType: 'string' },
        title: { bsonType: 'string' },
        description: { bsonType: 'string' },
        status: { enum: ['draft', 'spec_approved', 'architecture_done', 'code_complete', 'pr_merged'] },
        metaspecs: { bsonType: 'array' },
        context_budget: { bsonType: 'object' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('metaspecs');
db.createCollection('checkpoints');

// Criar índices para performance (IAD-7)
// projects collection
db.projects.createIndex({ id: 1 }, { unique: true });
db.projects.createIndex({ user_id: 1, created_at: -1 });

// demands collection
db.demands.createIndex({ id: 1 }, { unique: true });
db.demands.createIndex({ project_id: 1, status: 1 });
db.demands.createIndex({ project_id: 1, created_at: -1 });

// metaspecs collection
db.metaspecs.createIndex({ id: 1 }, { unique: true });
db.metaspecs.createIndex({ demand_id: 1, version: -1 });

// checkpoints collection
db.checkpoints.createIndex({ id: 1 }, { unique: true });
db.checkpoints.createIndex({ demand_id: 1, created_at: -1 });
db.checkpoints.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 }); // TTL index

// Criar usuário de aplicação (não root)
db.createUser({
  user: 'context_first_app',
  pwd: 'app_password_change_in_production',
  roles: [
    {
      role: 'readWrite',
      db: 'context_first_dev'
    }
  ]
});

print('✅ MongoDB initialization complete!');
print('Collections created: projects, demands, metaspecs, checkpoints');
print('Indexes created for performance (including unique indexes on id fields)');
print('Application user created: context_first_app');
