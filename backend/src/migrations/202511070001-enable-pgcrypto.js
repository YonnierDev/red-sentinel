'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    // Habilita extensión para generar UUIDs en Postgres
    await queryInterface.sequelize.query('CREATE EXTENSION IF NOT EXISTS "pgcrypto";');
  },

  async down(queryInterface, Sequelize) {
    // No eliminamos la extensión para evitar afectar otras tablas que ya dependan de ella
    // Si necesitas revertirla explícitamente, descomenta la siguiente línea bajo tu propia responsabilidad
    // await queryInterface.sequelize.query('DROP EXTENSION IF EXISTS "pgcrypto";');
  }
};
