'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('predictions', {
      id: {
        type: Sequelize.UUID,
        allowNull: false,
        primaryKey: true,
        defaultValue: Sequelize.literal('gen_random_uuid()')
      },
      user_id: {
        type: Sequelize.UUID,
        allowNull: true,
        references: { model: 'users', key: 'id' },
        onUpdate: 'SET NULL',
        onDelete: 'SET NULL'
      },
      model_id: {
        type: Sequelize.UUID,
        allowNull: false,
        references: { model: 'mlmodels', key: 'id' },
        onUpdate: 'CASCADE',
        onDelete: 'RESTRICT'
      },
      input_data: {
        type: Sequelize.JSONB,
        allowNull: false
      },
      output_data: {
        type: Sequelize.JSONB,
        allowNull: true
      },
      status: {
        type: Sequelize.ENUM('pending', 'processing', 'completed', 'failed'),
        allowNull: false,
        defaultValue: 'completed'
      },
      latency_ms: {
        type: Sequelize.INTEGER,
        allowNull: true
      },
      metadata: {
        type: Sequelize.JSONB,
        allowNull: true
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()')
      }
    });

    await queryInterface.addIndex('predictions', ['user_id']);
    await queryInterface.addIndex('predictions', ['status']);
    await queryInterface.addIndex('predictions', ['created_at']);
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('predictions');
    await queryInterface.sequelize.query("DROP TYPE IF EXISTS \"enum_predictions_status\";");
  }
};
