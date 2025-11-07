'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('audit_log', {
      id: {
        type: Sequelize.BIGINT,
        autoIncrement: true,
        primaryKey: true
      },
      user_id: {
        type: Sequelize.UUID,
        allowNull: true,
        references: { model: 'users', key: 'id' },
        onUpdate: 'SET NULL',
        onDelete: 'SET NULL'
      },
      action: {
        type: Sequelize.STRING(128),
        allowNull: false
      },
      entity_type: {
        type: Sequelize.STRING(64),
        allowNull: true
      },
      entity_id: {
        type: Sequelize.UUID,
        allowNull: true
      },
      old_values: {
        type: Sequelize.JSONB,
        allowNull: true
      },
      new_values: {
        type: Sequelize.JSONB,
        allowNull: true
      },
      ip_address: {
        type: Sequelize.INET,
        allowNull: true
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()')
      }
    });

    await queryInterface.addIndex('audit_log', ['user_id']);
    await queryInterface.addIndex('audit_log', ['entity_type']);
    await queryInterface.addIndex('audit_log', ['entity_id']);
    await queryInterface.addIndex('audit_log', ['created_at']);
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('audit_log');
  }
};
