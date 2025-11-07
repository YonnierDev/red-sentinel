'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('mlmodels', {
      id: {
        type: Sequelize.UUID,
        allowNull: false,
        primaryKey: true,
        defaultValue: Sequelize.literal('gen_random_uuid()')
      },
      name: {
        type: Sequelize.STRING(128),
        allowNull: false
      },
      version: {
        type: Sequelize.STRING(32),
        allowNull: false
      },
      path: {
        type: Sequelize.STRING(512),
        allowNull: false
      },
      metadata: {
        type: Sequelize.JSONB,
        allowNull: true
      },
      is_active: {
        type: Sequelize.BOOLEAN,
        allowNull: false,
        defaultValue: false
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()')
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()')
      }
    });

    await queryInterface.addIndex('mlmodels', ['name']);
    await queryInterface.addIndex('mlmodels', ['is_active']);
    await queryInterface.addConstraint('mlmodels', {
      fields: ['name', 'version'],
      type: 'unique',
      name: 'mlmodels_name_version_uk'
    });
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('mlmodels');
  }
};
